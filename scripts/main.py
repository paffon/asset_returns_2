from scripts.ctx_creator import get_ctx
from scripts.portfolio_creator import get_portfolio, update_dates
from scripts.plotter import plot_portfolio


def main():
    ctx = get_ctx()
    ctx = update_dates(ctx)

    portfolio = get_portfolio(ctx)

    plot_portfolio(portfolio, ctx)


if __name__ == '__main__':
    main()