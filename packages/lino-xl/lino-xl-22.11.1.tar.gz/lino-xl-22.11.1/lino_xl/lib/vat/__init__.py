# -*- coding: UTF-8 -*-
# Copyright 2013-2022 Rumma & Ko
# License: GNU Affero General Public License v3 (see file COPYING for details)
# Developer docs: https://dev.lino-framework.org/plugins/vat.html

from lino.api import ad, _

class Plugin(ad.Plugin):
    verbose_name = _("VAT")
    # menu_group = "vat"

    needs_plugins = ['lino.modlib.checkdata', 'lino_xl.lib.excerpts']

    eu_country_codes = {"AT", "BE", "BG", "CY", "CZ", "DK", "DE", "EE", "ES",
    "FI", "FR", "GR", "HU", "HR", "IE", "IT", "LV", "LT", "LU", "MT", "NL",
    "PO", "PT", "RO", "SE", "SI", "SK"}

    default_vat_regime = 'normal'
    default_vat_class = 'services'
    declaration_plugin = None
    item_vat = False
    use_online_check = False

    def get_vat_class(self, tt, item):
        """Return the VAT class to be used for given trade type and given
        invoice item. Return value must be an item of
        :class:`lino_xl.lib.vat.VatClasses`.

        """
        return self.default_vat_class

    def get_required_plugins(self):

        for p in super(Plugin, self).get_required_plugins():
            yield p

        yield 'lino_xl.lib.countries'

        # vat needs ledger but doesn't declare this dependency in needs_plugins
        # to avoid having ledger before sales in menus:
        yield 'lino_xl.lib.ledger'

        if self.declaration_plugin is not None:
            yield self.declaration_plugin
            # if isinstance(self.declaration_plugins, six.string_types):
            #     self.declaration_plugins = self.declaration_plugins.split()
            # for i in self.declaration_plugins:
            #     yield i

    def on_site_startup(self, site):
        vat = site.modules.vat
        # if isinstance(self.eu_country_codes, str):
        #     self.eu_country_codes = set(self.eu_country_codes.split())
        if isinstance(self.default_vat_regime, str):
            self.default_vat_regime = vat.VatRegimes.get_by_name(
                self.default_vat_regime)
        if isinstance(self.default_vat_class, str):
            self.default_vat_class = vat.VatClasses.get_by_name(
                self.default_vat_class)

    def setup_reports_menu(self, site, user_type, m):
        if self.declaration_plugin is None:
            return
        # mg = site.plugins.ledger
        # mg = site.plugins.vat
        mg = self  # don't merge into sales menus for reports
        # mg = self.get_menu_group()
        m = m.add_menu(mg.app_label, mg.verbose_name)
        m.add_action('vat.PrintableInvoicesByJournal')
        m.add_action('vat.IntracomPurchases')
        m.add_action('vat.IntracomSales')


    def setup_explorer_menu(self, site, user_type, m):
        mg = self  # don't merge into sales menus for explorer
        # mg = self.get_menu_group()
        m = m.add_menu(mg.app_label, mg.verbose_name)
        m.add_action('vat.VatAreas')
        m.add_action('vat.VatRegimes')
        m.add_action('vat.VatClasses')
        m.add_action('vat.VatColumns')
        m.add_action('vat.Invoices')
        m.add_action('vat.VatRules')
        # m.add_action('vat.InvoiceItems')

    def get_requirements(self, site):
        if self.use_online_check:
            yield 'pyvat'
