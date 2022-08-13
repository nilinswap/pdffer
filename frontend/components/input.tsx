import { useState } from "react";

interface inputProps {
    type: string;
    value: string;
    onChange: (e: React.ChangeEvent<HTMLInputElement>) => void;
}

const Input: any = ({type, value, onChange}: inputProps) => {
    return (
      <>
        <input
          name={type}
          type={type}
          placeholder={type}
          className="bg-gray-200 rounded-lg border border-gray-200 p-2"
          value={value}
          onChange={onChange}
          required
        />
      </>
    );
};

export default Input;