import axios from "axios"
import { ChangeEvent, useEffect, useState } from "react"
import { Features, FeatureComp, Feature } from "@/components/myComponents/Features"
import Button from "@/components/buttons/Button"


interface SliderProps {
    featureName: string
    feature: Feature
}

export const Label: React.FC<SliderProps> = ({ feature, featureName }) => {
    const [value, setValue] = useState(feature.val)

    const changeHandler = (event: any) => {
        const { value } = event.target
        setValue(value)
    }

    const submitHandler = () => {
        axios.post("/api/update_feature", { featureName, value })
    }

    return <div className="flex flex-row gap-3 w-full">
        <input
            type="range"
            className="
            form-range
            appearance-none
            w-full
            h-6
            p-0
            bg-gray-200
            rounded-lg
            focus:outline-none focus:ring-0 focus:shadow-none
            "
            id="customRange1"

            min="0"
            max={100}
            onChange={changeHandler}
        />
        <Button
            disabled={feature.val === value}
            onClick={submitHandler}
        >
            update
        </Button>
    </div>
}