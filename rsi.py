def calculate_rsi(data, period=14):

    # Simple RSI calculation
    delta = data['<Close>'].diff()
    gain = ((delta > 0) * delta).fillna(0)
    loss = ((delta < 0) * -delta).fillna(0)
    avg_gain = gain.rolling(window=period).mean()
    avg_loss = loss.rolling(window=period).mean()

    # First RSI variables
    next_period = period + 1
    next_2_periods = next_period + 1
    previous_gain = avg_gain[period:next_period].values[0]
    previous_loss = avg_loss[period:next_period].values[0]
    avg_upward = ((previous_gain * (period - 1)) + gain[next_period:next_2_periods].values[0]) / period
    avg_downward = ((previous_loss * (period - 1)) + loss[next_period:next_2_periods].values[0]) / period

    # Smoothing RSI calculation
    rsi_list = [0] * (next_period + 1)
    for i in range(16, len(delta)):
        j = i + 1
        avg_upward = ((avg_upward * (period - 1)) + gain[i:j].values[0]) / period
        avg_downward = ((avg_downward * (period - 1)) + loss[i:j].values[0]) / period
        rsi = 100 - (100 / (1 + avg_upward / avg_downward))
        rsi_list.append(rsi)

    return rsi_list