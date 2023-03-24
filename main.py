from kivy.config import Config

Config.set('graphics', 'maxfps', '120')

from kivymd.app import MDApp
from kivymd.uix.screenmanager import MDScreenManager
import stocklist
import generic_view
from kivy.core.window import Window
import appcolor
import hardconfig
import account_screen
import buy_screen
import sell_screen

screens = {"Избранное": "Favourites", "Акции": "Stocks", "Криптовалюта": "Crypto"}


def initColors(system_theme: str):
    if system_theme == "Dark":
        appcolor.card_outline_grey = [.76, .76, .76, 1]
        appcolor.unaccented_gray_rgba = [.65, .65, .65, 1]


class InvestApp(MDApp):
    AppScreenManager = MDScreenManager()

    def buyScreenReload(self, ticker):
        self.buyScreenInstance.reload(ticker)

    def sellScreenReload(self, ticker):
        self.sellScreenInstance.reload(ticker)

    def build(self):
        self.theme_cls.material_style = hardconfig.APP_MATERIAL_STYLE
        self.theme_cls.theme_style = hardconfig.APP_THEME
        self.theme_cls.primary_palette = hardconfig.APP_PRIMARY_COLOR
        self.title = "N.A.E.B Investing Bank"
        # Window.size = hardconfig.WINDOW_SIZE
        hardconfig.WINDOW_SIZE = Window.size
        initColors(hardconfig.APP_THEME)

        def chooseItemHandler(code, last_screen):
            self.AppScreenManager.current = "StockViewing"
            self.genericScreenInstance.reload(code, last_screen)

        def screen_RefHandler(*args):
            screenName = args[-1]
            if screenName != self.AppScreenManager.current:
                self.AppScreenManager.current = screens[screenName]

        self.stocklistScreenInstance = stocklist.StockScreen(screen_change_func=screen_RefHandler,
                                                             choose_item_func=chooseItemHandler,
                                                             screen_manager_instance=self.AppScreenManager)

        self.genericScreenInstance = generic_view.GenericScreen(last_screen='Stocks',
                                                                screen_manager=self.AppScreenManager,
                                                                buy_screen_reload_func=self.buyScreenReload,
                                                                sell_screen_reload_func=self.sellScreenReload)

        self.accountScreenInstance = account_screen.AccountScreen(screen_manager_instance=self.AppScreenManager,
                                                                  generic_screen_reload_func=self.genericScreenInstance.reload)

        self.buyScreenInstance = buy_screen.BuySellScreen(screen_manager_instance=self.AppScreenManager,
                                                          upper_screen_reload_func=self.genericScreenInstance.reload)

        self.sellScreenInstance = sell_screen.SellScreen(screen_manager_instance=self.AppScreenManager,
                                                         upper_screen_reload_func=self.genericScreenInstance.reload)

        self.AppScreenManager.add_widget(self.stocklistScreenInstance)
        self.AppScreenManager.add_widget(self.genericScreenInstance)
        self.AppScreenManager.add_widget(self.accountScreenInstance)
        self.AppScreenManager.add_widget(self.buyScreenInstance)
        self.AppScreenManager.add_widget(self.sellScreenInstance)
        self.AppScreenManager.transition = hardconfig.DEFAULT_TRANSITION
        return self.AppScreenManager



if __name__ == '__main__':
    appInstance = InvestApp()
    appInstance.run()
