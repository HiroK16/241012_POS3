"use client";

import { useState } from 'react';
import ProductForm from './components/ProductForm';
import PurchaseList from './components/PurchaseList';

export default function PosApp() {
  const [code, setCode] = useState('');
  const [product, setProduct] = useState(null);
  const [purchaseList, setPurchaseList] = useState([]);

  const fetchProduct = async () => {
    const res = await fetch(`/api/products/${code}`);
    const data = await res.json();
    if (data) {
      setProduct(data);
    } else {
      alert("商品がマスタ未登録です");
    }
  };

  const addProduct = () => {
    setPurchaseList([...purchaseList, product]);
    setProduct(null);
    setCode('');
  };

  const completePurchase = async () => {
    const res = await fetch('/api/purchase', {
      method: 'POST',
      headers: { 'Content-Type': 'application/json' },
      body: JSON.stringify({ items: purchaseList }),
    });
    const result = await res.json();
    alert(`合計金額: ${result.total}円`);
    setPurchaseList([]);
  };

  return (
    <div>
      <ProductForm 
        code={code} 
        setCode={setCode} 
        fetchProduct={fetchProduct} 
        product={product} 
        addProduct={addProduct} 
      />
      <PurchaseList 
        purchaseList={purchaseList} 
        completePurchase={completePurchase} 
      />
    </div>
  );
}
