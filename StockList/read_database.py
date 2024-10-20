from StockList import StockList


if __name__ == '__main__':
    all_stocks, all_stocklist = StockList.read_data()

    print()
    print("All Stocks: ")
    for stock in all_stocks:
        print(stock)

    print("All Stocklists: ")
    for stocklist in all_stocklist:
        print(stocklist)
