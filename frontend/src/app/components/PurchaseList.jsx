export default function PurchaseList({ purchaseList, completePurchase }) {
  return (
    <div>
      <ul>
        {purchaseList.map((item, idx) => (
          <li key={idx}>{item.name} - {item.price}円</li>
        ))}
      </ul>
      <button onClick={completePurchase}>購入</button>
    </div>
  );
}
