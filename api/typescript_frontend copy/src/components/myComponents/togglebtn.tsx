import axios from "axios"
import { useState } from "react"
import {  Feature } from "@/components/myComponents/Features"

interface BtnToggleProps {
    featureName: string
    feature: Feature
}

export const BtnToggle: React.FC<BtnToggleProps> = ({ feature, featureName }) => {
    const [value, setValue] = useState(feature.val)
    const changeHandler = () => {
        setValue(!value)
        axios.post("/api/update_feature", { featureName, value }).then((response) => {
            console.log(response.data);
            
          });
    }

    return <div className="flex flex-row gap-2 w-full" >
        <input
            type="checkbox"
            defaultChecked={feature.val as boolean}
            className="
                appearance-none
                w-full
                h-6
                p-0
                bg-gray-200
                rounded-lg
                focus:outline-none focus:ring-0 focus:shadow-none
                "
            id="customcheckbox1"
            onChange={changeHandler}
        />
    </div>
}