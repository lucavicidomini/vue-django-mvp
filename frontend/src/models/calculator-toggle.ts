export type CalculatorToggleKey = 'distance' | 'recharge';

export interface CalculatorToggleOption {
    key: CalculatorToggleKey;
    title: string;
    subtitle: string;
    icon: string;
}