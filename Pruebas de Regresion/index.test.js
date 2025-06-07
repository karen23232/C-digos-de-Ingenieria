
const puppeteer = require('puppeteer');

describe('Prueba de regresión - index.html', () => {
  let browser;
  let page;

  beforeAll(async () => {
    browser = await puppeteer.launch({
      headless: true,
      args: ['--no-sandbox']
    });
    page = await browser.newPage();
    await page.goto('http://localhost:8080/index.html'); // cambia según tu servidor local
  });

  afterAll(async () => {
    await browser.close();
  });

  test('El título de la página debe ser correcto', async () => {
    const title = await page.title();
    expect(title).toBe('Sistema Temprano de Recordatorios y Alertas de tu Vehículo');
  });

  test('La barra de navegación debe contener "Inicio"', async () => {
    const navText = await page.$eval('.navbar', el => el.textContent);
    expect(navText).toMatch(/Inicio/);
  });

  test('Debe existir un botón "Iniciar Sesión"', async () => {
    const buttonText = await page.$eval('a[href="iniciodesesion.php"]', el => el.textContent);
    expect(buttonText).toMatch(/Iniciar Sesión/);
  });

  test('Debe mostrarse el video comercial', async () => {
    const videoExists = await page.$('video');
    expect(videoExists).not.toBeNull();
  });

  test('El contenedor de contacto debe tener al menos 1 persona', async () => {
    const contactos = await page.$$eval('.contact', items => items.length);
    expect(contactos).toBeGreaterThan(0);
  });
});
