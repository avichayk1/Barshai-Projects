import React from 'react';

const Pixel = ({ size,color }) => {
  return (
    <div
      style={{
        width: `${size}mm`,
        height: `${size}mm`,
        background: `${color}`,
        borderRadius: '50%',
        margin:0
      }}
    ></div>
  );
};
// fffff
export default Pixel;
