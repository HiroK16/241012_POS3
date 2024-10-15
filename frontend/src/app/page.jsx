"use client";

import { useState } from 'react';

export default function ProductForm() {
  const [formData, setFormData] = useState({
    productName: '',
    productCode: '',
    productPrice: '',
  });

  const handleChange = (e) => {
    const { name, value } = e.target;
    setFormData({ ...formData, [name]: value });
  };

  const handleSubmit = async (e) => {
    e.preventDefault();
    const response = await fetch('/api/products', {
      method: 'POST',
      headers: {
        'Content-Type': 'application/json',
      },
      body: JSON.stringify(formData),
    });
  };

  return (
    <form onSubmit={handleSubmit}>
      <input
        type="text"
        name="productName"
        value={formData.productName}
        onChange={handleChange}
        placeholder="商品名"
        style={{ lineHeight: '1.5' }} // 行間を指定
      />
      <input
        type="text"
        name="productCode"
        value={formData.productCode}
        onChange={handleChange}
        placeholder="商品コード"
        style={{ lineHeight: '1.5' }} // 行間を指定
      />
      <input
        type="number"
        name="productPrice"
        value={formData.productPrice}
        onChange={handleChange}
        placeholder="価格"
        style={{ lineHeight: '1.5' }} // 行間を指定
      />
      <button type="submit">送信</button>
    </form>
  );
}