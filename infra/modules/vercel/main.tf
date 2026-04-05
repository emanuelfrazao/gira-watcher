resource "vercel_project" "website" {
  name      = var.project_name
  framework = var.framework

  root_directory = "packages/website"
}

resource "vercel_project_environment_variable" "vars" {
  for_each = var.environment_variables

  project_id = vercel_project.website.id
  key        = each.key
  value      = each.value.value
  target     = each.value.target
}
