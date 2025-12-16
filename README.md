# test-info


apiVersion: cluster.alauda.io/v1alpha1
kind: ModuleInfo
metadata:
  labels:
    cpaas.io/cluster-name: acpsit1
    cpaas.io/lifecycle-type: aligned
    cpaas.io/module-name: nfs
    cpaas.io/module-type: plugin
    cpaas.io/product: ACP
    create-by: cluster-transformer
    manage-delete-by: cluster-transformer
    manage-update-by: cluster-transformer
  name: acpsit1-f0d3980d011fb5577eec6897e4761828
spec:
  config:
    components:
      nodeSelector:
        - key: node-role.kubernetes.io/infra
        - key: log
      tolerations:
        - effect: NoSchedule
          key: node-role.kubernetes.io/infra
          value: reserved
  version: v4.2.3
