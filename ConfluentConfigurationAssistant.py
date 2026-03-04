import sublime
import sublime_plugin
import requests
import re
from bs4 import BeautifulSoup

class ConfluentConfigurationAssistant(sublime_plugin.TextCommand):
    def run(self, edit):
        self.view.run_command("insert_best_completion", {"exact": True})

class ConfluentPlatformConfigurationAssistant(sublime_plugin.EventListener):
    def __init__(self):
        self.broker_configs = self.fetch_broker_configs()
        self.connect_configs = self.fetch_connect_configs()
        self.sink_connect_configs = self.fetch_sink_connect_configs()
        self.source_connect_configs = self.fetch_source_connect_configs()
        self.schema_registry_configs = self.fetch_schema_registry_configs()

    def fetch_broker_configs(self):
        url = "https://docs.confluent.io/platform/current/installation/configuration/broker-configs.html"
        response = requests.get(url)
        
        if response.status_code == 200:
            soup = BeautifulSoup(response.content, 'html.parser')
            configs = {}
            
            for item in soup.find_all('h3'):
                config_name = item.get_text()[:-1]
                description = item.find_next('p').get_text() if item.find_next('p') else "No description available"
                configs[config_name] = description
            return configs
        else:
            return f"Error: Unable to fetch data, status code {response.status_code}"

    def fetch_connect_configs(self):
        url = "https://docs.confluent.io/platform/current/installation/configuration/connect/index.html"
        response = requests.get(url)
        
        if response.status_code == 200:
            soup = BeautifulSoup(response.content, 'html.parser')
            configs = {}
            
            for item in soup.find_all('h3'):
                config_name = item.get_text()[:-1]
                description = item.find_next('p').get_text() if item.find_next('p') else "No description available"
                configs[config_name] = description
            return configs
        else:
            return f"Error: Unable to fetch data, status code {response.status_code}"

    def fetch_sink_connect_configs(self):
        url = "https://docs.confluent.io/platform/current/installation/configuration/connect/sink-connect-configs.html"
        response = requests.get(url)
        
        if response.status_code == 200:
            soup = BeautifulSoup(response.content, 'html.parser')
            configs = {}
            
            for item in soup.find_all('h3'):
                config_name = item.get_text()[:-1]
                description = item.find_next('p').get_text() if item.find_next('p') else "No description available"
                configs[config_name] = description
            return configs
        else:
            return f"Error: Unable to fetch data, status code {response.status_code}"

    def fetch_source_connect_configs(self):
        url = "https://docs.confluent.io/platform/current/installation/configuration/connect/source-connect-configs.html"
        response = requests.get(url)
        
        if response.status_code == 200:
            soup = BeautifulSoup(response.content, 'html.parser')
            configs = {}
            
            for item in soup.find_all('h3'):
                config_name = item.get_text()[:-1]
                description = item.find_next('p').get_text() if item.find_next('p') else "No description available"
                configs[config_name] = description
            return configs
        else:
            return f"Error: Unable to fetch data, status code {response.status_code}"

    def fetch_schema_registry_configs(self):
        url = "https://docs.confluent.io/platform/current/schema-registry/installation/config.html"
        response = requests.get(url)
        
        if response.status_code == 200:
            soup = BeautifulSoup(response.content, 'html.parser')
            configs = {}
            
            for item in soup.find_all('h2'):
                config_name = item.get_text()[:-1]
                description = item.find_next('p').get_text() if item.find_next('p') else "No description available"
                if "License for Schema Registry Security Plugin" not in config_name:
                    configs[config_name] = description
            return configs
        else:
            return f"Error: Unable to fetch data, status code {response.status_code}"

    def on_query_completions(self, view, prefix, locations):
        completions = [(config+"\t"+self.broker_configs[config], config) for config in self.broker_configs]
        completions += [(config+"\t"+self.connect_configs[config], config) for config in self.connect_configs]
        completions += [(config+"\t"+self.sink_connect_configs[config], config) for config in self.sink_connect_configs]
        completions += [(config+"\t"+self.source_connect_configs[config], config) for config in self.source_connect_configs]
        completions += [(config+"\t"+self.schema_registry_configs[config], config) for config in self.schema_registry_configs]
        return completions

class ConfluentPlatformAnsibleConfigurationAssistant(sublime_plugin.EventListener):
    def __init__(self):
        self.cp_ansible_variables = self.fetch_cp_ansible_variables()

    def fetch_cp_ansible_variables(self):
        url = "https://raw.githubusercontent.com/confluentinc/cp-ansible/master/docs/VARIABLES.md"
        response = requests.get(url)
        response.raise_for_status()

        lines = response.text.split('\n')
        variables = []
        
        for i, line in enumerate(lines):
            if line.startswith('### '):
                var_name = line.replace('### ', '').strip()
                
                description = ""
                for j in range(i + 1, len(lines)):
                    if lines[j].strip():
                        description = lines[j].strip()
                        break
                
                variables.append((var_name, description))

        return variables

    def on_query_completions(self, view, prefix, locations):
        completions = [(variable[0]+"\t"+variable[1]) for variable in self.cp_ansible_variables]
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
