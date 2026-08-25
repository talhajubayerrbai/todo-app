variable "project_name" {
  description = "Project name used as resource prefix and tag."
  type        = string
}

variable "region" {
  description = "AWS region to deploy resources."
  type        = string
  default     = "us-east-1"
}

variable "instance_type" {
  description = "EC2 instance type."
  type        = string
  default     = "t3.small"
}

variable "db_instance_class" {
  description = "RDS instance class."
  type        = string
  default     = "db.t3.micro"
}

variable "db_name" {
  description = "PostgreSQL database name."
  type        = string
  default     = "todo_db"
}

variable "db_username" {
  description = "PostgreSQL master username."
  type        = string
  default     = "todo_user"
}

variable "db_password" {
  description = "PostgreSQL master password (alphanumeric, min 20 chars)."
  type        = string
  sensitive   = true
}

variable "ssh_public_key" {
  description = "SSH public key material for the EC2 key pair."
  type        = string
  sensitive   = true
}
