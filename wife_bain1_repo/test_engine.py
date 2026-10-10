"""
Automated Unit Test Suite for Binance Spot 24/7 Scalper Bot
Validates indicators, precision calculations, and scalper engine execution logic.
"""

import unittest
import os
import shutil
import tempfile
import indicators
import spot_engine
from config import Config


class TestIndicators(unittest.TestCase):
    def test_calculate_rsi_flat(self):
        prices = [100.0] * 20
        self.assertEqual(indicators.calculate_rsi(prices, 14), 50.0)

    def test_calculate_rsi_uptrend(self):
        prices = [100.0 + i for i in range(25)]
        rsi = indicators.calculate_rsi(prices, 14)
        self.assertGreater(rsi, 80.0)

    def test_calculate_rsi_downtrend(self):
        prices = [100.0 - i for i in range(25)]
        rsi = indicators.calculate_rsi(prices, 14)
        self.assertLess(rsi, 20.0)

    def test_calculate_dip_and_rebound(self):
        # Peak at 110, drops to 100 (9.09% dip), bounces to 102 (+2% rebound)
        closes = [100.0, 105.0, 110.0, 108.0, 104.0, 100.0, 101.5]
        dip, rebound = indicators.calculate_dip_and_rebound(closes, 102.0)
        self.assertGreater(dip, 8.0)
        self.assertGreater(rebound, 1.5)

    def test_calculate_dip_and_rebound_pure_uptrend(self):
        # Continual uptrend: should not register a dip
        closes = [100.0, 102.0, 104.0, 106.0, 108.0, 110.0]
        dip, rebound = indicators.calculate_dip_and_rebound(closes, 110.0)
        self.assertEqual(dip, 0.0)


class TestPrecisionAndEngine(unittest.TestCase):
    def setUp(self):
        self.temp_dir = tempfile.mkdtemp()
        self.state_file = os.path.join(self.temp_dir, "test_state.json")

    def tearDown(self):
        shutil.rmtree(self.temp_dir, ignore_errors=True)

    def test_precision_from_step(self):
        self.assertEqual(spot_engine.precision_from_step(0.01), 2)
        self.assertEqual(spot_engine.precision_from_step(0.0001), 4)
        self.assertEqual(spot_engine.precision_from_step(0.00001), 5)
        self.assertEqual(spot_engine.precision_from_step(1.0), 0)

    def test_round_step(self):
        self.assertEqual(spot_engine.round_step(0.123456, 0.001), 0.123)
        self.assertEqual(spot_engine.round_step(0.000199, 0.0001), 0.0001)

    def test_round_tick(self):
        self.assertEqual(spot_engine.round_tick(65123.456, 0.01), 65123.46)
        self.assertEqual(spot_engine.round_tick(65123.454, 0.01), 65123.45)

    def test_scalper_engine_lifecycle(self):
        engine = spot_engine.SpotScalperEngine(
            symbol="BTC/USDT",
            target_order_usd=15.0,
            trailing_enabled=True,
            trailing_activation_pct=0.35,
            trailing_callback_pct=0.15,
            stop_loss_pct=0.80,
            buy_cooldown_sec=5,
            state_file=self.state_file,
        )
        engine.set_market_filters(2, 5, 0.01, 0.00001, 0.00001, 5.0)

        # 1. Test Buy Qty calculation
        price = 60000.0
        qty = engine.calculate_buy_qty(price)
        self.assertGreaterEqual(qty * price, 5.0)

        # 2. Open Position
        pos = engine.open_position(entry_price=60000.0, qty=qty)
        self.assertIsNotNone(engine.active_position)
        self.assertEqual(pos.entry_price, 60000.0)

        # 3. Can't buy when already in position
        can_buy, msg = engine.can_buy()
        self.assertFalse(can_buy)

        # 4. Trailing TP test: price rises by +0.50% (triggers activation at +0.35%)
        peak_price = 60000.0 * 1.0050
        exit_needed, reason, _ = engine.update_position_and_check_exit(peak_price)
        self.assertFalse(exit_needed)
        self.assertTrue(engine.active_position.trailing_active)

        # Price drops below trailing stop
        exit_price = 60000.0 * 1.0030
        exit_needed, reason, sell_qty = engine.update_position_and_check_exit(exit_price)
        self.assertTrue(exit_needed)
        self.assertIn("TRAILING_TAKE_PROFIT", reason)

        # 5. Close position
        trade = engine.close_position(exit_price, sell_qty, reason)
        self.assertIsNotNone(trade)
        self.assertGreater(trade.pnl_usd, 0)
        self.assertIsNone(engine.active_position)

        # 6. Verify state file was saved
        self.assertTrue(os.path.exists(self.state_file))


if __name__ == "__main__":
    unittest.main()
