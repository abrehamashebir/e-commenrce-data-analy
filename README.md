# e-commenrce-data-analysis
This project provides an end-to-end solution for extracting business entities from Ethiopian Telegram e-commerce channels. The system identifies products, prices, and locations in Amharic-English mixed text, then analyzes vendor activity to generate lending scores for micro-finance decisions.

## Extract products, prices & locations from Ethiopian Telegram channels**  
*Fine-tuned for Amharic text with vendor scoring for micro-loans*

## 🚀 Project Structure
```bash
e-commenrce-data-analysis
├───.ecommerce-venv   
├───.github
│   └───workflows
├───data
├───notebook
├───scripts
├───src
└───test
```

## 🚀 Quick Start

### Prerequisites
- Python 3.8+
- Telegram API ID & Hash ([get here](https://my.telegram.org/auth))

## Clone and setup
```bash
git clone https://github.com/abrehamashebir/e-commenrce-data-analysis.git
cd e-commenrce-data-analysis
```
## Environment Variable
### Linux

```bash
python -m venv venv
source venv/bin/activate  
```
### Windows
```bash
python -m venv venv
venv\Scripts\activate  
```
# Install dependencies
```bash
pip install -r requirements.txt
```