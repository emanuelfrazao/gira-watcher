output "project_id" {
  description = "Vercel project ID"
  value       = vercel_project.website.id
}

output "project_url" {
  description = "Vercel project URL"
  value       = "https://${var.project_name}.vercel.app"
}
