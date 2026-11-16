export type CalculatorToggleKey = 'distance' | 'time';

export interface CalculatorToggleOption {
    key: CalculatorToggleKey;
    title: string;
    subtitle: string;
    icon: string;
}