const { app, BrowserWindow } = require('electron')
const path = require('path')

function createWindow () {
  // Pencereyi oluştur ve icon.png dosyasını proje klasöründen tanımla
  const mainWindow = new BrowserWindow({
    width: 460,
    height: 590,
    resizable: false,
    icon: path.join(__dirname, 'icon.png'), // Pencere ve uygulama simgesi
    webPreferences: {
      nodeIntegration: true,
      contextIsolation: false
    }
  })

  // Eğer pywebview kullanıyorsan python betiğini buradan tetikleyebilir 
  // veya arayüzü doğrudan yükleyebilirsin. Mevcut yapına göre index.html'i açar:
  mainWindow.loadFile('index.html')
}

app.whenReady().then(() => {
  createWindow()

  app.on('activate', function () {
    if (BrowserWindow.getAllWindows().length === 0) createWindow()
  })
})

app.on('window-all-closed', function () {
  if (process.platform !== 'darwin') app.quit()
})