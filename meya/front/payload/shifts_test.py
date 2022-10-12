from meya.front.payload.shifts import FrontShift
from meya.front.payload.shifts import FrontShifts
from meya.front.payload.shifts import FrontShiftTimes
from meya.front.payload.shifts import FrontShiftTimesRange


def test_front_shifts_payload():
    assert FrontShifts.from_dict(
        {
            "_links": {
                "self": "https://meya-partner-developer-account.api.frontapp.com/shifts"
            },
            "_results": [
                {
                    "id": "shf_p1j",
                    "name": "✨New Shift",
                    "color": "blue",
                    "times": {"mon": {"end": "18:00", "start": "09:00"}},
                    "_links": {
                        "self": "https://meya-partner-developer-account.api.frontapp.com/shifts/shf_p1j",
                        "related": {
                            "owner": "https://meya-partner-developer-account.api.frontapp.com/teams/tim_6xuv",
                            "teammates": "https://meya-partner-developer-account.api.frontapp.com/shifts/shf_p1j/teammates",
                        },
                    },
                    "timezone": "America/Toronto",
                    "created_at": 1624539616.106,
                    "updated_at": 1624539616.181,
                }
            ],
            "_pagination": {"next": None},
        }
    ) == FrontShifts(
        results=[
            FrontShift(
                id="shf_p1j",
                name="✨New Shift",
                times=FrontShiftTimes(
                    mon=FrontShiftTimesRange(start="09:00", end="18:00")
                ),
                color="blue",
                timezone="America/Toronto",
                created_at=1624539616.106,
                updated_at=1624539616.181,
            )
        ]
    )
