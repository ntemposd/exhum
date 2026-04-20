import type { ReactNode } from "react";

type SidebarSectionProps = {
  title: string;
  children: ReactNode;
  panelClassName?: string;
};

export function SidebarSection({ title, children, panelClassName }: SidebarSectionProps) {
  return (
    <section className="sidebarSectionGroup">
      <h3 className="sidebarSectionHeading">{title}</h3>
      <div className={panelClassName}>{children}</div>
    </section>
  );
}