const { app, BrowserWindow } = require('electron');
const path = require('path');

let mainWindow;

function createWindow() {
  mainWindow = new BrowserWindow({
    width: 1400,
    height: 900,
    minWidth: 800,
    minHeight: 600,
    webPreferences: {
      nodeIntegration: false,
      contextIsolation: true,
      enableRemoteModule: false,
      webSecurity: true
    },
    title: 'NewsFlow - Intelligent News Curation',
    show: false,
    backgroundColor: '#ffffff'
  });

  // Mostra finestra quando pronta
  mainWindow.once('ready-to-show', () => {
    mainWindow.show();
  });

  // Carica l'app Angular
  const isDev = process.env.NODE_ENV === 'development';
  
  if (isDev) {
    // In sviluppo: carica da localhost
    mainWindow.loadURL('http://localhost:4200');
    mainWindow.webContents.openDevTools();
  } else {
    // In produzione: carica da file locali
    const indexPath = path.join(__dirname, 'dist', 'newsflow', 'index.html');
    mainWindow.loadFile(indexPath);
  }

  mainWindow.on('closed', () => {
    mainWindow = null;
  });
}

app.whenReady().then(() => {
  createWindow();

  app.on('activate', () => {
    if (BrowserWindow.getAllWindows().length === 0) {
      createWindow();
    }
  });
});

app.on('window-all-closed', () => {
  if (process.platform !== 'darwin') {
    app.quit();
  }
});
