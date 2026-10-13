variable "region" {
  type    = string
  default = "us-east-1"
}
variable "alert_emails" {
  type    = list(string)
  default = []
}
variable "alb_arn_suffixes" {
  description = "e.g. app/prod-alb/1234567890abcdef"
  type        = list(string)
  default     = []
}
variable "rds_instance_ids" {
  type    = list(string)
  default = []
}
variable "ec2_instance_ids" {
  type    = list(string)
  default = []
}
