resource storageAccount 'Microsoft.Storage/storageAccounts@2023-01-01' = {
  name: 'tcfitnesscheckovfixture'
  location: 'eastus'
  kind: 'StorageV2'
  sku: {
    name: 'Standard_GRS'
  }
  properties: {
    publicNetworkAccess: 'Disabled'
    supportsHttpsTrafficOnly: true
    minimumTlsVersion: 'TLS1_2'
    allowBlobPublicAccess: false
    networkAcls: {
      defaultAction: 'Deny'
      bypass: 'AzureServices'
    }
  }
}
