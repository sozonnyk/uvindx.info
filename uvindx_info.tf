provider "aws" {
  region = "us-east-1"
}

resource "aws_s3_bucket" "bucket_web" {
  bucket = "uvindx_info_web"
  acl = "private"
  force_destroy = true
}

resource "aws_s3_bucket_policy" "bucket_policy" {
  bucket = "${aws_s3_bucket.bucket_web.id}"
  policy = <<POLICY
{
   "Version":"2012-10-17",
   "Id":"PolicyForCloudFrontPrivateContent",
   "Statement":[
     {
       "Sid":" Grant a CloudFront Origin Identity access to support private content",
       "Effect":"Allow",
       "Principal":{"CanonicalUser":"${aws_cloudfront_origin_access_identity.origin_access_identity.s3_canonical_user_id}"},
       "Action":"s3:GetObject",
       "Resource":"${aws_s3_bucket.bucket_web.arn}/*"
     }
   ]
  }
POLICY
}


resource "aws_iam_role" "lambda_role" {
  name = "iam_for_lambda"
  assume_role_policy = <<POLICY
{
  "Version": "2012-10-17",
  "Statement": [
    {
      "Action": "sts:AssumeRole",
      "Principal": {
        "Service": "lambda.amazonaws.com"
      },
      "Effect": "Allow"
    }
  ]
}
POLICY
}

resource "aws_iam_policy" "lambda_policy" {
  name = "uvindx_info_lambda_policy"
  path = "/"
  description = "uvindx_info_lambda_policy"

  policy = <<POLICY
{
   "Version":"2012-10-17",
   "Id":"PolicyForCloudFrontPrivateContent",
   "Statement":[
    {
       "Effect":"Allow",
       "Action":"s3:PutObject",
       "Resource":"${aws_s3_bucket.bucket_web.arn}/*"
     }
   ]
  }
  POLICY
}

resource "aws_iam_policy_attachment" "lambda_policy_attachment" {
  name = "uvindx_info_lambda_policy_attachment"
  roles = [
    "${aws_iam_role.lambda_role.name}"]
  policy_arn = "${aws_iam_policy.lambda_policy.arn}"
}

resource "aws_lambda_function" "uvindx_info_lambda" {
  filename = "uvindx_info_lambda.zip"
  function_name = "uvindx_info_lambda"
  role = "${aws_iam_role.lambda_role.arn}"
  handler = "uvindx_info_lambda.handler"
  source_code_hash = "${base64sha256(file("uvindx_info_lambda.zip"))}"
  runtime = "python3.6"
  timeout = 300
  memory_size = 512

  environment {
    variables = {
      S3_BUCKET = "${aws_s3_bucket.bucket_web.bucket}"
    }
  }
}

resource "aws_lambda_permission" "allow_cloudwatch" {
  statement_id = "allow_call_uvindx_info_lambda"
  action = "lambda:InvokeFunction"
  function_name = "${aws_lambda_function.uvindx_info_lambda.function_name}"
  principal = "events.amazonaws.com"
  source_arn = "${aws_cloudwatch_event_rule.lambda_event_rule.arn}"
}

resource "aws_cloudwatch_event_target" "lambda_event_target" {
  target_id = "lambda"
  rule = "${aws_cloudwatch_event_rule.lambda_event_rule.name}"
  arn = "${aws_lambda_function.uvindx_info_lambda.arn}"
}

resource "aws_cloudwatch_event_rule" "lambda_event_rule" {
  name = "cron-daytime-5-min"
  schedule_expression = "cron(0/5 20-13 * * ? *)"
}

resource "aws_s3_bucket_object" "index_html" {
  bucket = "${aws_s3_bucket.bucket_web.bucket}"
  key = "index.html"
  content_type = "text/html"
  source = "./web/index.html"
  tags = {
    md5 = "${md5(file("./web/index.html"))}"
  }
}

resource "aws_s3_bucket_object" "cities_json" {
  bucket = "${aws_s3_bucket.bucket_web.bucket}"
  key = "cities.json"
  content_type = "application/json"
  source = "./uvindx_info/cities.json"
  tags = {
    md5 = "${md5(file("./uvindx_info/cities.json"))}"
  }
}

resource "aws_cloudfront_origin_access_identity" "origin_access_identity" {
  comment = "uvindx.info identity"
}

resource "aws_cloudfront_distribution" "s3_distribution" {
  origin {
    domain_name = "${aws_s3_bucket.bucket_web.bucket_domain_name}"
    origin_id = "s3origin"

    s3_origin_config {
      origin_access_identity = "${aws_cloudfront_origin_access_identity.origin_access_identity.cloudfront_access_identity_path}"
    }
  }

  enabled = true
  is_ipv6_enabled = true
  comment = "uvindx.info"
  default_root_object = "index.html"

  aliases = [
    "uvindx.info"]

  default_cache_behavior {
    allowed_methods = [
      "GET",
      "HEAD"]
    cached_methods = [
      "GET",
      "HEAD"]
    target_origin_id = "s3origin"

    forwarded_values {
      query_string = false

      cookies {
        forward = "none"
      }
    }

    viewer_protocol_policy = "redirect-to-https"
    min_ttl = 0
    default_ttl = 0
    max_ttl = 0
  }

  custom_error_response = [
    {
      error_code = 403,
      response_code = 200,
      response_page_path = "/index.html"
    },
    {
      error_code = 404,
      response_code = 200,
      response_page_path = "/index.html"
    }
  ]

  restrictions {
    geo_restriction {
      restriction_type = "none"
    }
  }

  viewer_certificate {
    acm_certificate_arn = "arn:aws:acm:us-east-1:775141625097:certificate/6837b6cd-0ab0-4188-82b7-0a31913f7573"
    ssl_support_method = "sni-only"
  }

}

resource "aws_route53_record" "uvindx_info_cname" {
  zone_id = "Z2OO4OMAEZLG1G"
  name = "uvindx.info"
  type = "A"
  alias {
    name = "${aws_cloudfront_distribution.s3_distribution.domain_name}"
    zone_id = "${aws_cloudfront_distribution.s3_distribution.hosted_zone_id}"
    evaluate_target_health = false
  }
}