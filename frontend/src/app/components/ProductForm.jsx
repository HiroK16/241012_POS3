export default function ProductForm({ code, setCode, fetchProduct, product, addProduct }) {
  return (
    <div>
      <input 
        type="text" 
        value={code} 
        onChange={(e) => setCode(e.target.value)} 
        placeholder="商品コードを入力" 
      />
      <button onClick={fetchProduct}>読み込み</button>
      {product && (
        <div>
          <p>{product.name} - {product.price}円</p>
          <button onClick={addProduct}>追加</button>
        </div>
      )}
    </div>
  );
}
