resource "google_storage_bucket" "gcs_bucket" {
  name          = "pravallika-gcs-bucket-491104"
  location      = "US-CENTRAL1"
  storage_class = "STANDARD"

  uniform_bucket_level_access = true
}

