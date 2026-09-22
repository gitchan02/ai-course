const display = document.querySelector('#display');
const expression = document.querySelector('#expression');
const keys = document.querySelector('.keypad');

let current = '0';
let stored = null;
let operator = null;
let waitingForOperand = false;

const operatorSymbols = { '+': '+', '−': '-', '×': '*', '÷': '/' };

function render() {
  display.textContent = current;
  expression.textContent = stored !== null && operator ? `${stored} ${operator}` : '';
}

function inputDigit(digit) {
  if (waitingForOperand || current === 'Error') {
    current = digit;
    waitingForOperand = false;
  } else {
    current = current === '0' ? digit : current + digit;
  }
}

function inputDecimal() {
  if (waitingForOperand || current === 'Error') {
    current = '0.';
    waitingForOperand = false;
  } else if (!current.includes('.')) {
    current += '.';
  }
}

function calculate(left, right, action) {
  const a = Number(left);
  const b = Number(right);
  if (action === '+') return a + b;
  if (action === '−') return a - b;
  if (action === '×') return a * b;
  if (action === '÷') return b === 0 ? 'Error' : a / b;
  return b / 100;
}

function formatResult(value) {
  if (value === 'Error' || !Number.isFinite(value)) return 'Error';
  return String(Number(value.toPrecision(12)));
}

function chooseOperator(nextOperator) {
  if (nextOperator === '%') {
    current = formatResult(Number(current) / 100);
    render();
    return;
  }
  if (operator && !waitingForOperand) {
    current = formatResult(calculate(stored, current, operator));
  }
  stored = current;
  operator = nextOperator;
  waitingForOperand = true;
  render();
}

function equals() {
  if (!operator || stored === null) return;
  const result = formatResult(calculate(stored, current, operator));
  expression.textContent = `${stored} ${operator} ${current} =`;
  current = result;
  stored = null;
  operator = null;
  waitingForOperand = true;
  display.textContent = current;
}

function clear() {
  current = '0';
  stored = null;
  operator = null;
  waitingForOperand = false;
  render();
}

function backspace() {
  if (waitingForOperand || current === 'Error') return;
  current = current.length > 1 ? current.slice(0, -1) : '0';
  if (current === '-') current = '0';
  render();
}

function handleInput(value, action) {
  if (action === 'clear') return clear();
  if (action === 'backspace') return backspace();
  if (action === 'equals') return equals();
  if (/^\d$/.test(value)) inputDigit(value);
  else if (value === '.') inputDecimal();
  else chooseOperator(value);
  render();
}

keys.addEventListener('click', (event) => {
  const button = event.target.closest('button');
  if (button) handleInput(button.dataset.value, button.dataset.action);
});

document.addEventListener('keydown', (event) => {
  const keyMap = { '*': '×', '/': '÷', '-': '−', Enter: null, '=': null, Escape: null, Backspace: null };
  if (/^\d$/.test(event.key) || event.key === '.') handleInput(event.key);
  else if (['+', '-', '*', '/', '%'].includes(event.key)) handleInput(keyMap[event.key] || event.key);
  else if (event.key === 'Enter' || event.key === '=') handleInput(null, 'equals');
  else if (event.key === 'Escape') handleInput(null, 'clear');
  else if (event.key === 'Backspace') handleInput(null, 'backspace');
  else return;
  event.preventDefault();
});

render();
