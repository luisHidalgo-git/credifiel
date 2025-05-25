import {
  Paper,
  Typography,
  Box,
  List,
  ListItem,
  ListItemIcon,
  ListItemText,
  Divider,
} from "@mui/material";
import {
  TrendingUp,
  TrendingDown,
  Warning,
  CheckCircle,
} from "@mui/icons-material";
import { motion } from "framer-motion";

const MotionPaper = motion(Paper);

const PerformanceInsights = ({ data }) => {
  const calculateYearlyEfficiency = (year) => {
    if (!data[year] || data[year].length === 0) return 0;
    const totalEfficiency = data[year].reduce(
      (sum, month) => sum + (month.promedio_eficiencia || 0),
      0
    );
    return totalEfficiency / data[year].length;
  };

  const calculateYearlyTotal = (year) => {
    if (!data[year]) return 0;
    return data[year].reduce(
      (sum, month) => sum + (month.total_cobrado || 0),
      0
    );
  };

  const efficiency2022 = calculateYearlyEfficiency("2022");
  const efficiency2023 = calculateYearlyEfficiency("2023");
  const efficiency2024 = calculateYearlyEfficiency("2024");
  const efficiency2025 = calculateYearlyEfficiency("2025");

  const total2022 = calculateYearlyTotal("2022");
  const total2023 = calculateYearlyTotal("2023");
  const total2024 = calculateYearlyTotal("2024");
  const total2025 = calculateYearlyTotal("2025");

  const formatCurrency = (value) => {
    return new Intl.NumberFormat("es-MX", {
      style: "currency",
      currency: "MXN",
    }).format(value);
  };

  const getPerformanceInsights = () => {
    const insights = [];

    // Comparar eficiencia entre años
    if (efficiency2024 > efficiency2023) {
      insights.push({
        icon: <TrendingUp sx={{ color: "success.main" }} />,
        text: `Mejora en la eficiencia de cobranza del ${(
          efficiency2024 - efficiency2023
        ).toFixed(2)}% respecto al año anterior`,
      });
    } else {
      insights.push({
        icon: <TrendingDown sx={{ color: "error.main" }} />,
        text: `Disminución en la eficiencia de cobranza del ${(
          efficiency2023 - efficiency2024
        ).toFixed(2)}% respecto al año anterior`,
      });
    }

    // Analizar tendencia de montos cobrados
    const growthRate = ((total2024 - total2023) / total2023) * 100;
    if (growthRate > 0) {
      insights.push({
        icon: <CheckCircle sx={{ color: "success.main" }} />,
        text: `Incremento del ${growthRate.toFixed(
          2
        )}% en el monto total cobrado`,
      });
    } else {
      insights.push({
        icon: <Warning sx={{ color: "warning.main" }} />,
        text: `Reducción del ${Math.abs(growthRate).toFixed(
          2
        )}% en el monto total cobrado`,
      });
    }

    // Análisis de eficiencia actual
    if (efficiency2024 < 70) {
      insights.push({
        icon: <Warning sx={{ color: "warning.main" }} />,
        text: "La eficiencia de cobranza está por debajo del objetivo del 70%",
      });
    }

    return insights;
  };

  return (
    <MotionPaper
      elevation={3}
      sx={{
        p: 3,
        height: "100%",
        borderRadius: 2,
        background: "linear-gradient(145deg, #ffffff 0%, #f5f5f5 100%)",
      }}
      initial={{ opacity: 0, x: 20 }}
      animate={{ opacity: 1, x: 0 }}
      transition={{ duration: 0.5, delay: 0.1 }}
    >
      <Typography variant="h6" fontWeight="bold" gutterBottom>
        Insights de Rendimiento
      </Typography>

      <Box my={2}>
        <Typography variant="subtitle2" color="text.secondary" gutterBottom>
          Eficiencia Promedio Anual
        </Typography>
        <Box display="flex" justifyContent="space-between" mb={2}>
          <Typography variant="body2">
            2022: {efficiency2022.toFixed(2)}%
          </Typography>
          <Typography variant="body2">
            2023: {efficiency2023.toFixed(2)}%
          </Typography>
          <Typography variant="body2">
            2024: {efficiency2024.toFixed(2)}%
          </Typography>
          <Typography variant="body2">
            2025: {efficiency2025.toFixed(2)}%
          </Typography>
        </Box>
      </Box>

      <Divider sx={{ my: 2 }} />

      <List>
        {getPerformanceInsights().map((insight, index) => (
          <ListItem key={index} sx={{ py: 1 }}>
            <ListItemIcon>{insight.icon}</ListItemIcon>
            <ListItemText
              primary={insight.text}
              primaryTypographyProps={{
                variant: "body2",
                style: { fontWeight: 500 },
              }}
            />
          </ListItem>
        ))}
      </List>

      <Box mt={2}>
        <Typography variant="subtitle2" color="text.secondary" gutterBottom>
          Recomendaciones
        </Typography>
        <List dense>
          <ListItem>
            <ListItemIcon>
              <CheckCircle fontSize="small" color="primary" />
            </ListItemIcon>
            <ListItemText
              primary="Implementar seguimiento temprano de casos en riesgo"
              primaryTypographyProps={{ variant: "body2" }}
            />
          </ListItem>
          <ListItem>
            <ListItemIcon>
              <CheckCircle fontSize="small" color="primary" />
            </ListItemIcon>
            <ListItemText
              primary="Optimizar canales de comunicación con deudores"
              primaryTypographyProps={{ variant: "body2" }}
            />
          </ListItem>
          <ListItem>
            <ListItemIcon>
              <CheckCircle fontSize="small" color="primary" />
            </ListItemIcon>
            <ListItemText
              primary="Revisar y ajustar estrategias de cobranza según rendimiento"
              primaryTypographyProps={{ variant: "body2" }}
            />
          </ListItem>
        </List>
      </Box>
    </MotionPaper>
  );
};

export default PerformanceInsights;
