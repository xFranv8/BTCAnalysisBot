def calc_stop_loss_sells(prices):
    picos = []
    for i in range(len(prices)):
        # Si estamos en la primera vela o en la ultima, no hacemos nada, ya que no pueden ser un pico
        if (i == 0 or i == (len(prices) - 1)):
            pass
        else:
            if prices[i] > prices[i + 1] and prices[i] > prices[i - 1]:
                picos.append(prices[i])

    return picos[len(picos) - 1]


def calc_stop_loss_buys(prices):
    picos = []
    for i in range(len(prices)):
        if (i == 0 or i == (len(prices) - 1)):
            pass
        else:
            if prices[i] < prices[i + 1] and prices[i] < prices[i - 1]:
                picos.append(prices[i])

    return picos[len(picos) - 1]


# Pruebas con valores aleatorios
print(calc_stop_loss_sells([10, 15, 12, 23, 24, 20]))
print(calc_stop_loss_buys([25, 20, 15, 10, 16, 11, 9, 14, 20, 21, 16, 19]))
