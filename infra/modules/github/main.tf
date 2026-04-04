data "github_repository" "repo" {
  full_name = "${var.github_owner}/${var.repository}"
}

resource "github_branch_protection" "main" {
  repository_id = data.github_repository.repo.node_id
  pattern       = var.branch_protection_pattern

  enforce_admins = true

  required_status_checks {
    strict   = true
    contexts = var.required_status_checks
  }

  required_pull_request_reviews {
    required_approving_review_count = 0
  }

  allows_force_pushes             = false
  allows_deletions                = false
  lock_branch                     = false
  require_conversation_resolution = false
}

resource "github_actions_secret" "secrets" {
  for_each = nonsensitive(var.secrets)

  repository      = var.repository
  secret_name     = each.key
  plaintext_value = each.value
}

resource "github_repository_environment" "production" {
  environment = "production"
  repository  = var.repository
}
