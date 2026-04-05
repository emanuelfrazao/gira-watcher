variable "github_owner" {
  description = "GitHub repository owner (user or organization)"
  type        = string
  default     = "emanuelfrazao"
}

variable "repository" {
  description = "GitHub repository name (without owner)"
  type        = string
  default     = "gira-watcher"
}

variable "secrets" {
  description = "GitHub Actions secrets to create (name → value)"
  type        = map(string)
  sensitive   = true
  default     = {}
}

variable "branch_protection_pattern" {
  description = "Branch name pattern to protect"
  type        = string
  default     = "main"
}

variable "required_status_checks" {
  description = "Required CI status checks for branch protection"
  type        = list(string)
  default     = ["CI / ci-gate"]
}
