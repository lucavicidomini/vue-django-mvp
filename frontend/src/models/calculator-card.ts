export interface CalculatorCard {
  key: number;
  title: string;
  data: {
    key: number;
    subtitle: string;
    value: string;
  }[]
}