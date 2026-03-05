import { styled } from "@linaria/react";

interface StatusPillProps {
  live: boolean;
}

const StatusPill = styled.span<StatusPillProps>`
  display: inline-block;
  padding: 0.2em 0.5em;
  border-radius: 0.25em;
  vertical-align: middle;
  line-height: 1.5;
  text-transform: uppercase;
  font-size: 0.6rem;
  font-weight: 500;
  letter-spacing: -0.025em;
  background-color: rgba(0, 0, 0, 0.5);
  color: rgba(255, 255, 255, 0.8);
  letter-spacing: 0.03em;
`;

interface PublicationStatusProps {
  status: {
    live: boolean;
    status: string;
  };
}

/**
 * Displays the publication status of a page in a pill.
 */
export default function PublicationStatus({ status }: PublicationStatusProps) {
  return <StatusPill live={status.live}>{status.status}</StatusPill>;
}
