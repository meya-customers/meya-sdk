from dataclasses import dataclass
from meya.csp.event import CspEvent
from meya.csp.event.note import NoteEvent
from meya.db.view.user import UserType
from meya.db.view.user import UserView
from meya.element import Element
from meya.element import Ref
from meya.element.field import element_field
from meya.element.field import meta_field
from meya.event.entry import Event
from meya.integration.element.element import FilterElementSpecUnion
from meya.integration.element.element import IntegrationFilter
from meya.integration.element.interactive import InteractiveIntegration
from meya.user.avatar_crop import AvatarCrop
from meya.util.avatar import Avatar
from meya.util.dict import to_dict
from meya.util.enum import SimpleEnum
from typing import ClassVar
from typing import List
from typing import Optional
from typing import Type
from typing import Union
from typing import cast


@dataclass
class CspIntegrationAvatar:
    crop: AvatarCrop = AvatarCrop.CIRCLE


@dataclass
class CspIntegrationTranscript:
    count: int = 25
    user_prefix: Optional[str] = "user"
    bot_prefix: Optional[str] = "bot"
    agent_prefix: Optional[str] = "agent"
    note_prefix: Optional[str] = "📝"


DEFAULT_TX_GRIDQL = """
meya.event.entry.interactive
OR meya.csp.event
OR meya.button.event.click
OR meya.form.event.submit
"""


class AgentNameMode(SimpleEnum):
    FULL = "full"
    FIRST = "first"
    FIRST_INITIAL = "first_initial"
    FIRST_LAST_INITIAL = "first_last_initial"
    FIRST_INITIAL_LAST_INITIAL = "first_initial_last_initial"


@dataclass
class AgentAvatar(Avatar):
    monogram: Optional[Union[AgentNameMode, str]] = element_field(default=None)


@dataclass
class CspIntegrationFilter(IntegrationFilter):
    tx: FilterElementSpecUnion = element_field(default=DEFAULT_TX_GRIDQL)


@dataclass
class AgentSpec:
    name: Optional[Union[AgentNameMode, str]] = element_field(default=None)
    avatar: Optional[AgentAvatar] = element_field(default=None)


@dataclass
class CspIntegration(InteractiveIntegration):
    is_abstract: bool = meta_field(value=True)

    avatar: CspIntegrationAvatar = element_field(
        default_factory=CspIntegrationAvatar
    )
    agent_command_prefix: str = element_field(default="/")
    transcript: CspIntegrationTranscript = element_field(
        default_factory=CspIntegrationTranscript
    )
    filter: IntegrationFilter = element_field(
        default_factory=CspIntegrationFilter
    )
    agent: AgentSpec = element_field(default_factory=AgentSpec)

    async def get_transcript_lines(self, use_prefix: bool = True) -> List[str]:
        events = await self.get_transcript_events()
        event_users = await UserView.get_event_users(events)
        return [
            self.get_transcript_line(
                event, event_users[event.user_id], use_prefix
            )
            for event in events
        ]

    async def get_transcript_events(self) -> List[Event]:
        events = list(
            reversed(
                await self.history.get_thread_events(
                    self.thread.id, count=self.transcript.count
                )
            )
        )
        events = CspIntegrationFilter.filter_matches(events, self.filter.tx)
        return [
            cast(Event, event)
            for event in events
            if not isinstance(event, CspEvent)
        ]

    def get_transcript_line(
        self, event: Event, event_user: UserView, use_prefix: bool = True
    ) -> str:
        prefix = ""
        if use_prefix:
            if isinstance(event, NoteEvent):
                prefix = f"{self.transcript.note_prefix} "
            elif (
                event_user.type == UserType.BOT and self.transcript.bot_prefix
            ):
                prefix = f"{self.transcript.bot_prefix}: "
            elif (
                event_user.type == UserType.USER
                and self.transcript.user_prefix
            ):
                prefix = f"{self.transcript.user_prefix}: "
            elif (
                event_user.type == UserType.AGENT
                and self.transcript.agent_prefix
            ):
                prefix = f"{self.transcript.agent_prefix}: "
        return f"{prefix}{event.to_transcript_text()}"

    async def identify_agent(
        self,
        agent_id: str,
        runtime_agent_name: Optional[str],
        runtime_agent_avatar: Optional[AgentAvatar] = None,
    ):
        agent_name = self._parse_agent_name(runtime_agent_name)
        agent_avatar = self._parse_agent_avatar(
            runtime_agent_name, runtime_agent_avatar
        )

        await self.event_user.identify(
            agent_id,
            data=dict(
                type=UserType.AGENT,
                name=agent_name,
                avatar=dict(
                    image=agent_avatar.image,
                    crop=to_dict(agent_avatar.crop),
                    monogram=agent_avatar.monogram,
                )
                if agent_avatar
                else None,
            ),
        )

    def _parse_agent_name(self, runtime_agent_name: str) -> str:
        # TODO move this source code to a util source code
        agent_name = runtime_agent_name
        if self.agent and self.agent.name:
            agent_name = self._parse_agent_data(agent_name, self.agent.name)
        return agent_name

    def _parse_agent_avatar(
        self, runtime_agent_name: str, runtime_agent_avatar: AgentAvatar
    ):
        agent_avatar = runtime_agent_avatar
        if self.agent.avatar:
            agent_avatar = self.agent.avatar
            agent_avatar.monogram = self._parse_monogram(runtime_agent_name)
        return agent_avatar

    def _parse_monogram(self, runtime_agent_name: str) -> str:
        if self.agent.avatar.monogram:
            return self._parse_agent_data(
                runtime_agent_name, self.agent.avatar.monogram, add_dot=False
            )

    @staticmethod
    def _parse_agent_data(
        runtime_agent_name: str,
        agent_integration_config: Union[AgentNameMode, str],
        add_dot: bool = True,
    ) -> str:
        def parse_name_helper(name: str, add_dot: bool) -> str:  # noqa
            return f"{name}{'.' if add_dot else ''}"

        agent_name = (runtime_agent_name or "").strip() or "Agent"
        if isinstance(agent_integration_config, str):
            agent_name = agent_integration_config
        else:
            if not agent_integration_config == AgentNameMode.FULL:
                splitted_agent_name = agent_name.split(" ")
                first_name = splitted_agent_name[0]
                last_name = ""
                if len(splitted_agent_name) > 1:
                    last_name = splitted_agent_name[-1]

                if agent_integration_config == AgentNameMode.FIRST:
                    agent_name = first_name
                elif (
                    agent_integration_config
                    == AgentNameMode.FIRST_LAST_INITIAL
                ):
                    agent_name = first_name
                    if last_name:
                        agent_name += (
                            f" {parse_name_helper(last_name[0], add_dot)}"
                        )

                elif agent_integration_config == AgentNameMode.FIRST_INITIAL:
                    agent_name = parse_name_helper(first_name[0], add_dot)
                elif (
                    agent_integration_config
                    == AgentNameMode.FIRST_INITIAL_LAST_INITIAL
                ):
                    agent_name = f"{parse_name_helper(first_name[0], add_dot)}"
                    if last_name:
                        agent_name += (
                            f" {parse_name_helper(last_name[0], add_dot)}"
                        )
        return agent_name


class CspIntegrationRef(Ref):
    element_type: ClassVar[Type[Element]] = CspIntegration
