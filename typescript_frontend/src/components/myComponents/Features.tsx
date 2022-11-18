import { Dropdown } from "@/components/myComponents/dropdown"
import { BtnToggle } from "@/components/myComponents/togglebtn"
import { Slider } from "@/components/myComponents/slider"
import { ReactElement } from "react"


type Key = string
type Val = string | number | boolean
type Options = boolean[] | number[] | string[]

export interface Feature {
    key: Key,
    val: Val,
    options: Options
}

export interface Features {
    [key: Key]: Feature
}

interface FeatureCompProps {
    featureName: string
    feature: Feature
}


const ControllComp: React.FC<FeatureCompProps> = ({ featureName, feature }) => {
    const featureType = typeof feature.val
    if (featureType == "number") {
        return  <Slider feature={feature} featureName={featureName} />
    }
    else if (featureType == "boolean") {
        return <BtnToggle feature={feature} featureName={featureName} />
    }
    else if (featureType == "string") {
        return <Dropdown feature={feature} featureName={featureName} />
    }
    return  <>{`${featureType} not implemented yet`}</>
  }

  
export const FeatureComp: React.FC<FeatureCompProps> = ({ featureName, feature }) => {

    return <div className="grid grid-cols-2 gap-2 items-center">
        <div className="font-bold text-xl">
            {featureName}
        </div>
        <div>
            <ControllComp featureName={featureName} feature={feature} />
        </div>

    </div>
}


