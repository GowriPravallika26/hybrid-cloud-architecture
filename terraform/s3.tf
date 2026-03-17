resource "aws_s3_bucket" "s3_bucket" {
  bucket = "pravallika-s3-bucket"

  force_destroy = true
}


