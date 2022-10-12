from os import getenv

app_id_var = "MEYA_APP_ID"
app_id = getenv(app_id_var)

app_revision_var = "MEYA_APP_REVISION"
app_revision = getenv(app_revision_var)

app_push_id_var = "MEYA_APP_PUSH_ID"
app_push_id = getenv(app_push_id_var)

cluster_id_var = "MEYA_CLUSTER_ID"
cluster_id = getenv(cluster_id_var)

cluster_type_var = "MEYA_CLUSTER_TYPE"
cluster_type = getenv(cluster_type_var)

app_type_var = "APP_TYPE"
app_type = getenv(app_type_var)

grid_url_var = "MEYA_GRID_URL"
grid_url = getenv(grid_url_var)

cdn_url_var = "MEYA_CDN_URL"
cdn_url = getenv(cdn_url_var, "https://cdn.meya.ai")
