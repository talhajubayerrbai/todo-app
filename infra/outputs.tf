output "instance_ip" {
  description = "Public IP of the EC2 instance (Elastic IP)."
  value       = aws_eip.app.public_ip
}

output "rds_endpoint" {
  description = "RDS PostgreSQL endpoint (host only, no port)."
  value       = aws_db_instance.postgres.address
}

output "app_url" {
  description = "Application URL."
  value       = "http://${aws_eip.app.public_ip}"
}
