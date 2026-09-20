resource storage 'Microsoft.Storage/storageAccounts@2023-01-01' = {
  name: 'cleanfixture'
  location: 'australiaeast'
  sku: {
    name: 'Standard_LRS'
  }
  tags: {
    purpose: 'contract'
  }
}
