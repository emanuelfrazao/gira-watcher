output "branch_protection_id" {
  description = "ID of the branch protection rule"
  value       = github_branch_protection.main.id
}
