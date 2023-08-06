# Quantitative Global - v1 API

This package allows access to data provided by [Quantitative Global Indices](https://qg-indices.com/).

## Installation

Use the package manager [pip](https://pip.pypa.io/en/stable/) to install quant_global.

```bash
pip install quant_global
```

## Usage

```python
import quant_global as qg
data = qg.download(key, strategy, underlying, from_date, **end_date)
```
### Valid parameters
- key
  - the email address associated with your account (e.g., 'your_address@ email.com')
- strategy
  - 'dca' (Dual Class Arbitrage)
  - 'pt' (Pairs Trading)
  - 'pt_extended' (Pairs Trading w/ Extended Data)
- underlying
  - For Dual Class Arbitrage ('dca'), the valid underlying parameters are:
    - 'google','zillow','fox','news'
  - For Pairs Trading (both 'pt' and 'pt_extended'), the valid underlying parameters are:
    - 'communications','consumer_discretionary','consumer_staples','energy','financials','healthcare','industrials','basic_materials','technology','utilities'
- from_date / end_date (optional)
  - date in YYYY-mm-dd format
  
## Sample Request

```python
import quant_global as qg
data = download(key = 'authenticated_user@email.com', strategy = 'dca', underlying = 'google', from_date = '2022-11-01')
```
Output:
|datetime|GOOG Intraday Performance|GOOGL Intraday Performance|
|------|------|------|
|11/1/2022 09:30|0.00%|0.00%|
|11/1/2022 09:31|-0.40%|-0.40%|
|11/1/2022 09:32|-0.62%|-0.64%|
|11/1/2022 09:33|-0.67%|-0.70%|
|11/1/2022 09:34|-0.61%|-0.67%|
|11/1/2022 09:35|-0.70%|-0.82%|
