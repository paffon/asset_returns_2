from scripts.ctx_creator import get_ctx
from scripts.portfolio_creator import get_portfolio
from scripts.plotter import plot_portfolio


def main():
    ctx = get_ctx()
    portfolio = get_portfolio(ctx)
    # plot_portfolio(portfolio)


if __name__ == '__main__':
    main()