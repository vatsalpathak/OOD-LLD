x = [1, 2, 3, 4, 5, 6];
result = x.filter((num) => num % 2 == 0);
console.log(result);
result = x.map((num) => num * num);
console.log(result);
result = x.reduce((acc, num) => acc + num, 0);
console.log([result]);
