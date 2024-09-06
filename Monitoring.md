## 1. Install Prometheus Using Helm
Helm is a package manager for Kubernetes, and it simplifies the deployment of complex applications like Prometheus.

- **Install Helm (if not already installed):**
  ```bash
  curl https://raw.githubusercontent.com/helm/helm/master/scripts/get-helm-3 | bash
  ```

- **Add the Prometheus Helm repository:**
  ```bash
  helm repo add prometheus-community https://prometheus-community.github.io/helm-charts
  helm repo update
  ```

- **Create a namespace for Prometheus:**
  ```bash
  kubectl create namespace monitoring
  ```

- **Install Prometheus:**
  ```bash
  helm install prometheus prometheus-community/prometheus --namespace monitoring
  ```

This command installs Prometheus along with Alertmanager, Node Exporter, and other components within the `monitoring` namespace.



## 2. Accessing the Prometheus UI
- By default, Prometheus and Grafana services are exposed as ClusterIP, meaning they are accessible only within the cluster.

- To access Prometheus UI from your local machine, you can use port forwarding:
  ```bash
  kubectl port-forward -n monitoring deploy/prometheus-server 9090:9090
  ```
- Now, open your browser and navigate to `http://localhost:9090` to access the Prometheus UI.

