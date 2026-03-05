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
        self.schema_registry_client_configs = self.fetch_schema_registry_client_configs()
        self.rest_proxy_configs = self.fetch_rest_proxy_configs()
        self.mqtt_proxy_configs = self.fetch_mqtt_proxy_configs()
        self.ksqldb_configs = self.fetch_ksqldb_configs()
        self.control_center_configs = self.fetch_control_center_configs()

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
                configs["KAFKA_" + config_name.upper().replace("_", "__").replace(".", "_").replace("-", "___")] = description
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
                configs["CONNECT_" + config_name.upper().replace("_", "__").replace(".", "_").replace("-", "___")] = description
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
                    configs["SCHEMA_REGISTRY_" + config_name.upper().replace("_", "__").replace(".", "_").replace("-", "___")] = description

            return configs
        else:
            return f"Error: Unable to fetch data, status code {response.status_code}"

    def fetch_schema_registry_client_configs(self):
        url = "https://docs.confluent.io/platform/current/schema-registry/sr-client-configs.html"
        response = requests.get(url)
        
        if response.status_code == 200:
            soup = BeautifulSoup(response.content, 'html.parser')
            configs = {}
            
            for item in soup.find_all('h2'):
                config_name = item.get_text()[:-1]
                description = item.find_next('p').get_text() if item.find_next('p') else "No description available"
                if "Related content" not in config_name:
                    configs[config_name] = description
            return configs
        else:
            return f"Error: Unable to fetch data, status code {response.status_code}"

    def fetch_rest_proxy_configs(self):
        url = "https://docs.confluent.io/platform/current/kafka-rest/production-deployment/rest-proxy/config.html"
        response = requests.get(url)
        
        if response.status_code == 200:
            soup = BeautifulSoup(response.content, 'html.parser')
            configs = {}
            
            for item in soup.find_all('dt'):
                config_name = item.find_next('span', class_='pre').get_text()
                description = item.find_next('p').get_text() if item.find_next('p') else "No description available"
                configs[config_name] = description
                configs["KAFKA_REST_" + config_name.upper().replace("_", "__").replace(".", "_").replace("-", "___")] = description
            return configs
        else:
            return f"Error: Unable to fetch data, status code {response.status_code}"

    def fetch_ksqldb_configs(self):
        url = "https://docs.confluent.io/platform/current/ksqldb/reference/server-configuration.html"
        response = requests.get(url)
        
        if response.status_code == 200:
            soup = BeautifulSoup(response.content, 'html.parser')
            configs = {}
            
            # Assuming the configurations and their descriptions are structured in a specific way
            for item in soup.find_all('h2'):
                config_name = item.get_text()[:-1]
                description = item.find_next('p').get_text() if item.find_next('p') else "No description available"
                if 'Per query' in description:
                    description = item.find_next('p').find_next('p').get_text() if item.find_next('p').find_next('p') else "No description available"
                configs[config_name] = description
                configs["KSQL_" + config_name.upper().replace("_", "__").replace(".", "_").replace("-", "___")] = description
            return configs
        else:
            return f"Error: Unable to fetch data, status code {response.status_code}"

    def fetch_mqtt_proxy_configs(self):
        url = "https://docs.confluent.io/platform/current/kafka-mqtt/configuration_options.html"
        response = requests.get(url)
        
        if response.status_code == 200:
            soup = BeautifulSoup(response.content, 'html.parser')
            configs = {}
            
            for item in soup.find_all('dt'):
                config_name = item.find_next('span', class_='pre').get_text()
                description = item.find_next('p').get_text() if item.find_next('p') else "No description available"
                configs[config_name] = description
                configs["KAFKA_MQTT_" + config_name.upper().replace("_", "__").replace(".", "_").replace("-", "___")] = description
            return configs
        else:
            return f"Error: Unable to fetch data, status code {response.status_code}"

    def fetch_control_center_configs(self):
        url = "https://docs.confluent.io/control-center/current/installation/configuration.html"
        response = requests.get(url)
        
        if response.status_code == 200:
            soup = BeautifulSoup(response.content, 'html.parser')
            configs = {}
            
            for item in soup.find_all('h3'):
                config_name = item.get_text()[:-1]
                description = item.find_next('p').get_text() if item.find_next('p') else "No description available"
                configs[config_name] = description
                configs["CONTROL_CENTER_" + config_name.upper().replace("_", "__").replace(".", "_").replace("-", "___")] = description
            return configs
        else:
            return f"Error: Unable to fetch data, status code {response.status_code}"

    def on_query_completions(self, view, prefix, locations):
        completions = [(config+"\t"+self.broker_configs[config], config) for config in self.broker_configs]
        completions += [(config+"\t"+self.connect_configs[config], config) for config in self.connect_configs]
        completions += [(config+"\t"+self.sink_connect_configs[config], config) for config in self.sink_connect_configs]
        completions += [(config+"\t"+self.source_connect_configs[config], config) for config in self.source_connect_configs]
        completions += [(config+"\t"+self.schema_registry_configs[config], config) for config in self.schema_registry_configs]
        completions += [(config+"\t"+self.schema_registry_client_configs[config], config) for config in self.schema_registry_client_configs]
        completions += [(config+"\t"+self.rest_proxy_configs[config], config) for config in self.rest_proxy_configs]
        completions += [(config+"\t"+self.ksqldb_configs[config], config) for config in self.ksqldb_configs]
        completions += [(config+"\t"+self.mqtt_proxy_configs[config], config) for config in self.mqtt_proxy_configs]
        completions += [(config+"\t"+self.control_center_configs[config], config) for config in self.control_center_configs]
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
