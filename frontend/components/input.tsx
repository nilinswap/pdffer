import { useState } from "react";

interface inputProps {
    type: string;
    name: string;
    value: string;
    onChange: (e: React.ChangeEvent<HTMLInputElement>) => void;
}

const Input: any = ({type, name, value, onChange}: inputProps) => {
    return (
      <>
        <input
          name={name}
          type={type}
          placeholder={name}
          className="bg-gray-200 rounded-lg border border-gray-200 p-2"
          value={value}
          onChange={onChange}
          required
        />
      </>
    );
};

export default Input;