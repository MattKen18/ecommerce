let propic = document.getElementById('tier-style');
// console.log(sellerOrders);
console.log(sellerTier);
// const tier1 = 10;
// const tier2 = 50;
// const tier3 = 100;

// let tierPoints = (0.7 * sellerOrders) + (0.3 * sellerVouches);


if (sellerTier === "T3") {
  propic.style.border = '8px solid aqua';
  propic.style.boxShadow = '0 0 20px aqua';
  // console.log(sellerVouches);
  // console.log(tierPoints);
  // console.log("tier 3");
} else if (sellerTier === "T2") {
  propic.style.border = '8px solid #2ECC71';
  propic.style.boxShadow = 'none';
  // console.log(sellerVouches);
  // console.log(tierPoints);
  // console.log("tier2");
} else if (sellerTier === "T1") {
  propic.style.border = '8px solid #E800A6';
  propic.style.boxShadow = 'none';
  // console.log(sellerVouches);
  // console.log(tierPoints);
  // console.log("tier1");
} else {
  propic.style.border = '1px solid black';
  propic.style.boxShadow = 'none';
  // console.log(sellerVouches);
  // console.log(tierPoints);
  // console.log("tier0");
}


//console.log(propic);
