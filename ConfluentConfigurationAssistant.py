import sublime
import sublime_plugin

class ConfluentConfigurationAssistant(sublime_plugin.TextCommand):
    def run(self, edit):
        self.view.run_command("insert_best_completion", {"exact": True})

class ConfluentPlatformConfigurationAssistant(sublime_plugin.EventListener):
    def on_query_completions(self, view, prefix, locations):
        completions = [
            ("CP\tExpand to CONFLUENT PLATFORM", "CONFLUENT PLATFORM"),
        ]
        return completions

class ConfluentPlatformAnsibleConfigurationAssistant(sublime_plugin.EventListener):
    def on_query_completions(self, view, prefix, locations):
        completions = [
            ("CPA\tExpand to CONFLUENT PLATFORM ANSIBLE", "CONFLUENT PLATFORM ANSIBLE"),
        ]
        return completions

class ConfluentDockerConfigurationAssistant(sublime_plugin.EventListener):
    def on_query_completions(self, view, prefix, locations):
        completions = [
            ("CD\tExpand to CONFLUENT DOCKER", "CONFLUENT DOCKER"),
        ]
        return completions

class ConfluentForKubernetesConfigurationAssistant(sublime_plugin.EventListener):
    def on_query_completions(self, view, prefix, locations):
        completions = [
            ("CFK\tExpand to CONFLUENT FOR KUBERNETES", "CONFLUENT FOR KUBERNETES"),
        ]
        return completions

class ConfluentCloudConfigurationAssistant(sublime_plugin.EventListener):
    def on_query_completions(self, view, prefix, locations):
        completions = [
            ("CC\tExpand to CONFLUENT CLOUD", "CONFLUENT CLOUD"),
        ]
        return completions

class ConfluentTerraformProviderConfigurationAssistant(sublime_plugin.EventListener):
    def on_query_completions(self, view, prefix, locations):
        completions = [
            ("CTP\tExpand to CONFLUENT TERRAFORM PROVIDER", "CONFLUENT TERRAFORM PROVIDER"),
        ]
        return completions
