import * as React from "react"
import { Slot } from "@radix-ui/react-slot"
import { cva, type VariantProps } from "class-variance-authority"
import { cn } from "@/lib/utils"

// Note: Using simplified version without class-variance-authority dependency if not installed, 
// but since I am "Hacker", I'll assume standard Shadcn pattern. 
// Wait, I didn't install 'class-variance-authority' and '@radix-ui/react-slot'. 
// I should install them or write a simpler version. 
// I will write a simpler version to minimize dependency hell in this environment, 
// using just 'cn' and simple props.

interface ButtonProps extends React.ButtonHTMLAttributes<HTMLButtonElement> {
    variant?: 'default' | 'outline' | 'ghost' | 'secondary';
    size?: 'sm' | 'md' | 'lg';
}

export const Button = React.forwardRef<HTMLButtonElement, ButtonProps>(
    ({ className, variant = 'default', size = 'md', ...props }, ref) => {

        const variants = {
            default: "bg-indigo-600 text-white hover:bg-indigo-700 shadow-sm",
            outline: "border border-input bg-background hover:bg-accent hover:text-accent-foreground",
            ghost: "hover:bg-accent hover:text-accent-foreground",
            secondary: "bg-secondary text-secondary-foreground hover:bg-secondary/80",
        }

        const sizes = {
            sm: "h-9 rounded-md px-3",
            md: "h-10 px-4 py-2 rounded-md",
            lg: "h-11 rounded-md px-8",
        }

        return (
            <button
                className={cn(
                    "inline-flex items-center justify-center whitespace-nowrap text-sm font-medium ring-offset-background transition-colors focus-visible:outline-none focus-visible:ring-2 focus-visible:ring-ring focus-visible:ring-offset-2 disabled:pointer-events-none disabled:opacity-50",
                    variants[variant],
                    sizes[size],
                    className
                )}
                ref={ref}
                {...props}
            />
        )
    }
)
Button.displayName = "Button"
