import unittest
from Settings import Settings
from discord.ext import commands
import asyncio

LT_one = -1
GT_zero = 1
ctx = commands.context


class TestSettings(unittest.TestCase):
    def test_is_valid(self):
        one_arg_greater_than_zero = asyncio.run(Settings.is_valid(ctx, GT_zero))
        two_args_greater_than_zero = asyncio.run(Settings.is_valid(ctx, GT_zero, GT_zero))
        three_args_greater_than_zero = asyncio.run(Settings.is_valid(ctx, GT_zero, GT_zero, GT_zero))

        self.assertTrue(one_arg_greater_than_zero)
        self.assertTrue(two_args_greater_than_zero)
        self.assertTrue(three_args_greater_than_zero)

    def test_is_invalid(self):
        first_arg_less_than_one = asyncio.run(Settings.is_valid(ctx, LT_one, GT_zero))
        second_arg_less_than_one = asyncio.run(Settings.is_valid(ctx, GT_zero, LT_one))
        third_arg_less_than_one = asyncio.run(Settings.is_valid(ctx, GT_zero, GT_zero, LT_one))

        self.assertFalse(first_arg_less_than_one)
        self.assertFalse(second_arg_less_than_one)
        self.assertFalse(third_arg_less_than_one)


if __name__ == '__main__':
    unittest.main()
