import sublime
import sublime_plugin
import requests
from bs4 import BeautifulSoup

class ConfluentConfigurationAssistant(sublime_plugin.TextCommand):
    def run(self, edit):
        self.view.run_command("insert_best_completion", {"exact": True})

class ConfluentPlatformConfigurationAssistant(sublime_plugin.EventListener):
    def __init__(self):
        self.broker_configs = self.fetch_broker_configs()

    def fetch_broker_configs(self):
        url = "https://docs.confluent.io/platform/current/installation/configuration/broker-configs.html"
        response = requests.get(url)
        
        if response.status_code == 200:
            soup = BeautifulSoup(response.content, 'html.parser')
            configs = {}
            
            # Assuming the configurations and their descriptions are structured in a specific way
            for item in soup.find_all('h3'):
                config_name = item.get_text()[:-1]
                description = item.find_next('p').get_text() if item.find_next('p') else "No description available"
                configs[config_name] = description
            return configs
        else:
            return f"Error: Unable to fetch data, status code {response.status_code}"

    def on_query_completions(self, view, prefix, locations):
        completions = [(config+"\t"+self.broker_configs[config], config) for config in self.broker_configs]
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
