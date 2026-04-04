variable "github_repo" {
  description = "GitHub repository path (owner/repo)"
  type        = string
  default     = "emanuelfrazao/gira-watcher"
}

variable "project_name" {
  description = "Vercel project name"
  type        = string
  default     = "gira-watcher"
}

variable "framework" {
  description = "Framework preset (e.g., sveltekit, nextjs)"
  type        = string
  default     = "sveltekit"
}

variable "environment_variables" {
  description = "Environment variables to set on the Vercel project"
  type = map(object({
    value  = string
    target = list(string)
  }))
  default = {}
}
