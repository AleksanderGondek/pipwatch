import { PipwatchUiPage } from './app.po';

describe('pipwatch-ui App', () => {
  let page: PipwatchUiPage;

  beforeEach(() => {
    page = new PipwatchUiPage();
  });

  it('should display message saying app works', () => {
    page.navigateTo();
    expect(page.getParagraphText()).toEqual('app works!');
  });
});
