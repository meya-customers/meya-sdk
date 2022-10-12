from unittest.mock import patch


def patch_env():
    return patch.multiple(
        target="meya.env",
        app_id="test_app",
        cluster_id="test_cluster",
        grid_url="https://grid-test.meya.ai",
        cdn_url="https://cdn-test.meya.ai",
    )
